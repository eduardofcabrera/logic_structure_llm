

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c d)
(on d a)
(on e c)
(clear b)
)
(:goal
(and
(on a c)
(on b d)
(on e b))
)
)


