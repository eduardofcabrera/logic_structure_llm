

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(on c d)
(ontable d)
(on e a)
(clear c)
(clear e)
)
(:goal
(and
(on a e)
(on c a)
(on d b))
)
)


