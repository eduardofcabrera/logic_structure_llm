

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c d)
(ontable d)
(on e c)
(clear b)
(clear e)
)
(:goal
(and
(on a b)
(on d a))
)
)


