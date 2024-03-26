

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(on c a)
(ontable d)
(on e c)
(clear b)
(clear e)
)
(:goal
(and
(on a c)
(on b e)
(on d b)
(on e a))
)
)


