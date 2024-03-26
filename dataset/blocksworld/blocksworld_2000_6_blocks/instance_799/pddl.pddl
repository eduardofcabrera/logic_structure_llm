

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(ontable c)
(on d b)
(on e c)
(clear a)
(clear e)
)
(:goal
(and
(on a e)
(on b d)
(on c a))
)
)


